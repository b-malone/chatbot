from gensim.models import TfidfModel, LdaModel, LsiModel
import config as cfg
import utils


def build_lda_model(dictionary, corpus, should_rebuild):
    lda = list()

    # DEBUG
    should_rebuild = True

    # debug_print('datapath:LDA', datapath(cfg.LDA_BACKUP))

    if not should_rebuild:
        try:
            print('Loading LDA Model backup...')
            lda_file = utils.get_file_path(cfg.LDA_BACKUP)
            print('LDA file = {}'.format(lda_file))

            lda = LdaModel.load(lda_file)

        except Exception as exc:
           utils.print_exception_details('Building LDA Model', exc)

    else:
        print('Building LDA Model...')
        lda = LdaModel(corpus, id2word=dictionary, random_state=cfg.RANDOM_STATE, num_topics=cfg.NUM_TOPICS, passes=cfg.NUM_PASSES)
        print('Done!')
        # Save Model Structures
        LDA_FILE = utils.get_file_path(cfg.LDA_BACKUP)
        lda.save(LDA_FILE)

    return lda

def build_lsi_model(dictionary, corpus, should_rebuild):
    lsi = list()

    # DEBUG
    should_rebuild = True

    if not should_rebuild:
        try:
            print('Loading LSI Model backup...')
            lsi_file = utils.get_file_path(cfg.LDA_BACKUP)
            print('LSI file = {}'.format(lsi_file))

            lsi = LdaModel.load(lsi_file)

        except Exception as exc:
           utils.print_exception_details('Building LSI Model', exc)

    else:
        print('Building LSI Model...')
        one_pass = cfg.NUM_PASSES > 1
        lsi = LsiModel(corpus, id2word=dictionary, num_topics=cfg.NUM_TOPICS, onepass=one_pass)
        print('Done!')
        # Save Model Structures
        LSI_FILE = utils.get_file_path(cfg.LSI_BACKUP)
        lsi.save(LSI_FILE)

    return lsi

def build_tfid_model(dictionary, corpus, should_rebuild):
    tfid = list()

    # DEBUG
    should_rebuild = True

    if not should_rebuild:
        try:
            print('Loading TFID Model backup...')
            tfid_file = utils.get_file_path(cfg.TFID_BACKUP)
            print('TFID file = {}'.format(tfid_file))

            tfid = LdaModel.load(tfid_file)

        except Exception as exc:
           utils.print_exception_details('Building TFID Model', exc)

    else:
        print('Building TFID Model...')
        tfid = TfidfModel(corpus)
        print('Done!')
        # Save Model Structures
        TFID_FILE = utils.get_file_path(cfg.TFID_BACKUP)
        tfid.save(TFID_FILE)

    return tfid

