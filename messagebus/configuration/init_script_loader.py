import glob
import logging

def load_init_scripts(path, context):
    """
    Load scripts from a directory and call their "init" functions, passing
    in a context object
    """

    logger = logging.getLogger("InitScriptLoader")

    for filename in glob.glob(path + "/*.py"):
        logger.debug("Load %s", filename)

        script = load_script(filename)
        if script.has_key("init"):
            init_function = script["init"]
            init_function(context)

    logger.info("Finished loading init scripts")

def load_script(filename):
    namespace = {}
    execfile(filename, namespace)
    return namespace