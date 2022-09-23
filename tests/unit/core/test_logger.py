from trafalgar_log.core.logger import Logger


def test_info():
    Logger.info("a", "a", "")


def test_debug():
    Logger.debug("a", "a", "")


def test_warn():
    Logger.warn("a", "a", "")


def test_error():
    Logger.error("a", "a", "")


def test_critical():
    Logger.critical("a", "a", "")


def test_set_correlation_id():
    Logger.set_correlation_id("a")


def test_get_correlation_id():
    Logger.get_correlation_id()


def test_set_flow():
    Logger.set_flow("a")


def test_get_flow():
    Logger.get_flow()


def test_set_instance_id():
    Logger.set_instance_id("a")


def test_get_instance_id():
    Logger.get_instance_id()
