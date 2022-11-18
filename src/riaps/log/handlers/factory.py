
import riaps.log.handlers.tmux as tmux_handler
import riaps.log.handlers.testing_handler as test_handler


def get_handler(handler_type, **kwargs):
    server_log_handler = None
    if handler_type == "tmux":
        server_log_handler = _get_tmux_handler(handler_type, **kwargs)
    elif handler_type == "testing":
        server_log_handler = _get_testing_handler(handler_type, **kwargs)

    return server_log_handler


def _get_tmux_handler(handler_type, session_name):
    server_log_handler = tmux_handler.ServerLogHandler(handler_type, session_name)
    return server_log_handler


def _get_testing_handler(handler_type, test_data):
    server_log_handler = test_handler.ServerLogHandler(handler_type, test_data)
    return server_log_handler


