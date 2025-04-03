from pydantic_settings import BaseSettings, SettingsConfigDict


class OpenAISettings(BaseSettings):
    """
    Settings for OpenAI API.

    Attributes:
        API_KEY (str): OpenAI API key.
        ASSISTANT_ID (str): OpenAI Assistant ID.
    """
    model_config = SettingsConfigDict(
        env_file=".env",
        extra='ignore',
        env_prefix="OPENAI_",
    )

    API_KEY: str
    ASSISTANT_ID: str


class StreamlitSystemSettings(BaseSettings):
    """
    Settings for Streamlit system.

    Attributes:
        PORT (int): Streamlit server port.
        PASSWORD (str): Password for Streamlit authentication.
    """
    model_config = SettingsConfigDict(
        env_file=".env",
        extra='ignore',
        env_prefix="STREAMLIT_SYSTEM_",
    )

    PORT: int
    PASSWORD: str


class StreamlitTextsSettings(BaseSettings):
    """
    Settings for Streamlit texts.

    Attributes:
        PASSWORD_REQUEST (str): Text for password request.
        PASSWORD_INCORRECT (str): Text for incorrect password.
        TITLE (str): Title of the Streamlit app.
        CHAT_INPUT (str): Text for chat input.
    """
    model_config = SettingsConfigDict(
        env_file=".env",
        extra='ignore',
        env_prefix="STREAMLIT_TEXTS_",
    )

    PASSWORD_REQUEST: str
    PASSWORD_INCORRECT: str
    TITLE: str
    CHAT_INPUT: str


class Settings(BaseSettings):
    """
    Main settings class that aggregates all settings.

    Attributes:
        openai (OpenAISettings): OpenAI API settings.
        streamlit_system (StreamlitSystemSettings): Streamlit system settings.
        streamlit_texts (StreamlitTextsSettings): Streamlit texts settings.
    """
    openai: OpenAISettings = OpenAISettings()
    streamlit_system: StreamlitSystemSettings = StreamlitSystemSettings()
    streamlit_texts: StreamlitTextsSettings = StreamlitTextsSettings()


settings = Settings()
