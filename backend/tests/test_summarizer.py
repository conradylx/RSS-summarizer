from unittest.mock import patch, MagicMock


class TestSummarize:
    """Tests for the summarize function"""

    def test_empty_text_returns_empty_string(self):
        from app.services.summarizer import summarize

        result = summarize("")
        assert result == ""

    def test_none_text_returns_empty_string(self):
        from app.services.summarizer import summarize

        result = summarize(None)  # type: ignore
        assert result == ""

    @patch("app.services.summarizer.client")
    def test_successful_summarization(self, mock_client):
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "This is a summary."
        mock_client.chat.completions.create.return_value = mock_response

        from app.services.summarizer import summarize

        result = summarize("Some long article text here...")

        assert result == "This is a summary."
        mock_client.chat.completions.create.assert_called_once()

    @patch("app.services.summarizer.client")
    def test_api_error_returns_empty_string(self, mock_client):
        mock_client.chat.completions.create.side_effect = Exception(
            "Connection refused"
        )

        from app.services.summarizer import summarize

        result = summarize("Some text")

        assert result == ""

    @patch("app.services.summarizer.client")
    def test_text_is_truncated_to_1000_chars(self, mock_client):
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Summary"
        mock_client.chat.completions.create.return_value = mock_response

        from app.services.summarizer import summarize

        long_text = "a" * 2000
        summarize(long_text)

        call_args = mock_client.chat.completions.create.call_args
        user_message = call_args.kwargs["messages"][1]["content"]
        assert len(user_message) == 1000
