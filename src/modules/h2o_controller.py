import h2o

def init_h2o():
    h2o.init(verbose=False)
    # print(h2o.cluster().show_status())
    h2o.no_progress()

    h_objects = h2o.ls()
    for key in [x for x in h_objects.key if x != 'S3_CREDENTIALS_KEY']:
        # print(f'Removing key {key}')
        h2o.remove(key)

    return h2o

def shutdown_h2o(h2o):
    h2o.shutdown()
