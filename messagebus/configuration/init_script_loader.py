import glob
import logging

scripts = []

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
            scripts.append(script)
            init_function = script["init"]
            init_function(context)

    logger.info("Finished loading init scripts")

def shutdown_scripts():

    logger = logging.getLogger("InitScriptLoader")
    logger.info("Shutting down init_scripts")
    for script in scripts:
        if script.has_key("shutdown"):
            shutdown_function = script["shutdown"]
            shutdown_function()
    logger.info("Shut down all init_scripts")

def load_script(filename):
    namespace = {}
    execfile(filename, namespace)
    return namespace