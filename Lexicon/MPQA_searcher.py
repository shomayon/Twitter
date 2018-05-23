import mpqa
from utils import utils








def main():
    utterance = "I had a good day today."
    ret = mpqa.lookup(word="good", original_pos="anypos")
    print(ret)


if __name__=="__main__":
    mpqa.load_data("../resources/lexicons/subjectivity_clues_hltemnlp05/subjclueslen1-HLTEMNLP05.tff")
    main()