import traceback

try:
    import inference
    inference.main()
except Exception as e:
    with open("error_log.txt", "w") as f:
        f.write(traceback.format_exc())
