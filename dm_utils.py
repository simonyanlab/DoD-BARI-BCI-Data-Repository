import numpy as np

def meta_accuracy(correct, decisions, confidence, max_confidence=4):
    """
    Compute metacognitive accuracy over a set of trials.
    :params correct: correct decision
    :params decisions: decisions of the subject
    :params confidence: confidence of the subject
    """
    correctness = np.array(correct) == np.array(decisions)
    score = 0
    for trial in range(len(correct)):
        if correctness[trial]:
            score += confidence[trial] / max_confidence
        else:
            score += 1 - confidence[trial] / max_confidence
    return score / len(correct)

def accuracy(correct, decisions):
    """
    Compute accuracy over a set of trials.
    :params correct: correct decision
    :params decisions: decisions of the subject
    """
    correctness = np.array(correct) == np.array(decisions)
    return sum(correctness) / len(correctness) * 100
