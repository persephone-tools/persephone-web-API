from unittest.mock import Mock

def test_create_corpus_file_structure(tmpdir):
    """Test filesystem tasks related to corpus creation"""
    from api.corpus import create_corpus_file_structure
    test_dir = str(tmpdir.mkdir("corpus_filesystem_test"))
    mock_corpus = Mock(spec_set=["id","name","training", "testing", "validation"])
    mock_corpus.id = 1
    mock_corpus.name = "mock corpus"
    mock_corpus.training = ['0']
    mock_corpus.testing = ['1']
    mock_corpus.validation = ['2']
    create_corpus_file_structure(mock_corpus, test_dir)

    train_prefixes_path = os.path.join(test_dir, "train_prefixes.txt")
    test_prefixes_path = os.path.join(test_dir, "test_prefixes.txt")
    valid_prefixes_path = os.path.join(test_dir, "valid_prefixes.txt")
    
    assert os.path.is_file(train_prefixes_path)
    assert os.path.is_file(test_prefixes_path)
    assert os.path.is_file(valid_prefixes_path)