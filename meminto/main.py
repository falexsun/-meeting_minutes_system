import os
from pathlib import Path
import click
from meminto.llm.tokenizers import Tokenizer
from meminto.audio_processing import split_audio
from meminto.decorators import log_time
from meminto.diarizer import Diarizer
from meminto.helpers import (
    Language,
    load_pkl,
    parse_input_file_path,
    parse_output_folder_path,
    save_as_pkl,
    select_language,
    write_text_to_file,
)
from meminto.llm.ollama_llm import OllamaLLM
from meminto.llm.lmstudio_llm import LMStudioLLM
from meminto.meeting_minutes_generator import (
    MeetingMinutesGenerator,
)
from meminto.transcriber import LocalTranscriber
from dotenv import load_dotenv

EXAMPLE_INPUT_FILE = Path(__file__).parent.resolve() / "../examples/Scoreboard.wav"
DEFAULT_OUTPUT_FOLDER = Path(__file__).parent.resolve() / "../output"
DEFAULT_LANGUAGE = Language.RUSSIAN


@click.command()
@click.option(
    "-f",
    "--input-file",
    show_default=True,
    default=EXAMPLE_INPUT_FILE,
    help="Path to the input audio file.",
)
@click.option(
    "-o",
    "--output-folder",
    show_default=True,
    default=DEFAULT_OUTPUT_FOLDER,
    help="Path to the folder where the output files are stored.",
)
@click.option(
    "-l",
    "--language",
    show_default=True,
    default=DEFAULT_LANGUAGE,
    help="Select the language in which the meeting minutes should be generated. Currently supproted are 'english' and 'russian'.",
)
@click.option(
    "-lm",
    "--use-lmstudio",
    is_flag=True,
    show_default=True,
    default=True,
    help="If selected the Meminto will use LM Studio for local LLM. The enviroment variable 'LMSTUDIO_MODEL' needs to be set.",
)
def main(
    input_file: str, output_folder: str, language: str, use_lmstudio: bool
) -> None:
    load_dotenv()
    audio_input_file_path = parse_input_file_path(input_file)
    output_folder_path = parse_output_folder_path(output_folder)
    selected_language = select_language(language)
    
    # Принудительно использовать только локальные модели
    print("⚠️  ВНИМАНИЕ: Используются только локальные модели")
    print("⚠️  Данные НЕ передаются на внешние сервисы")
    print("⏱️  Таймаут обработки: 1 час")
    print("\n" + "="*50 + "\n")
    
    create_meeting_minutes(
        audio_input_file_path, output_folder_path, selected_language, use_lmstudio
    )


@log_time
def create_meeting_minutes(
    audio_input_file_path: Path,
    output_folder_path: Path,
    language: Language,
    use_lmstudio: bool,
):
    ### Diarization (локально) ###
    print("🔒 Диаризация: используется локальная модель pyannote")
    print("⏳ Начинается анализ аудио...")
    diarizer = Diarizer(
        model="pyannote/speaker-diarization@2.1",
        hugging_face_token=os.environ["HUGGING_FACE_ACCESS_TOKEN"],
    )
    diarization = diarizer.diarize_audio(audio_input_file_path)

    diarization_text = diarizer.diarization_to_text(diarization)
    write_text_to_file(diarization_text, output_folder_path / "diarization.txt")
    save_as_pkl(diarization, output_folder_path / "diarization.pkl")
    print("✅ Диаризация завершена\n")

    ### Transcription (локально) ###
    diarization = load_pkl(output_folder_path / "diarization.pkl")
    audio_sections = split_audio(audio_input_file_path, diarization)

    print("🔒 Транскрипция: используется локальная модель Whisper")
    print("⏳ Начинается транскрипция (это может занять несколько минут)...")
    transcriber = LocalTranscriber()
    transcript = transcriber.transcribe(audio_sections)

    transcript_text = transcriber.transcript_to_txt(transcript)
    write_text_to_file(transcript_text, output_folder_path / "transcript.txt")
    save_as_pkl(transcript, output_folder_path / "transcript.pkl")
    print("✅ Транскрипция завершена\n")

    ### Generation (локально) ###
    if use_lmstudio:
        print("🔒 Генерация протокола: используется локальная LLM через LM Studio")
        print("⏳ Это может занять несколько минут в зависимости от размера протокола...")
        model_name = os.environ.get("LMSTUDIO_MODEL", "local-model")
        lmstudio_url = os.environ.get("LMSTUDIO_URL", "http://localhost:1234/v1/chat/completions")
        max_tokens = int(os.environ.get("LMSTUDIO_MAX_TOKENS", "8000"))

        tokenizer = Tokenizer(
            model_name,
            hugging_face_acces_token=os.environ.get("HUGGING_FACE_ACCESS_TOKEN", ""),
        )

        llm = LMStudioLLM(
            model=model_name,
            url=lmstudio_url,
            temperature=0.5,
            max_tokens=max_tokens,
        )
    else:
        print("🔒 Генерация протокола: используется локальная LLM через Ollama")
        print("⏳ Это может занять несколько минут в зависимости от размера протокола...")
        model_name = os.environ.get("OLLAMA_MODEL", "qwen2.5:7b")
        ollama_url = os.environ.get("OLLAMA_URL", "http://localhost:11434/api/generate")
        max_tokens = int(os.environ.get("OLLAMA_MAX_TOKENS", "8000"))

        tokenizer = Tokenizer(
            model_name,
            hugging_face_acces_token=os.environ.get("HUGGING_FACE_ACCESS_TOKEN", ""),
        )

        llm = OllamaLLM(
            model=model_name,
            url=ollama_url,
            temperature=0.5,
            max_tokens=max_tokens,
        )

    transcript = load_pkl(output_folder_path / "transcript.pkl")
    meeting_minutes_generator = MeetingMinutesGenerator(tokenizer=tokenizer, llm=llm)
    meeting_minutes = meeting_minutes_generator.generate(
        transcript=transcript, language=language
    )

    write_text_to_file(meeting_minutes, output_folder_path / "meeting_minutes.txt")
    print("✅ Протокол совещания успешно создан (полностью локально)")
    print(f"📁 Файл сохранен: {output_folder_path / 'meeting_minutes.txt'}")


if __name__ == "__main__":
    main()
