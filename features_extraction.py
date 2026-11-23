
import re
import string


def extract_features(password):
    """
    Extract numerical features from a password
    for Machine Learning classification.
    """

    features = {}

    # Basic password length
    features["length"] = len(password)

    # Character composition
    features["uppercase_count"] = sum(
        1 for char in password if char.isupper()
    )

    features["lowercase_count"] = sum(
        1 for char in password if char.islower()
    )

    features["digit_count"] = sum(
        1 for char in password if char.isdigit()
    )

    features["special_count"] = sum(
        1 for char in password if char in string.punctuation
    )

    # Character type indicators
    features["has_uppercase"] = int(any(
        char.isupper() for char in password
    ))

    features["has_lowercase"] = int(any(
        char.islower() for char in password
    ))

    features["has_digit"] = int(any(
        char.isdigit() for char in password
    ))

    features["has_special"] = int(any(
        char in string.punctuation for char in password
    ))

    # Repeated character indicator
    features["has_repeated_chars"] = int(
        bool(re.search(r"(.)\1", password))
    )

    # Simple sequential pattern indicator
    sequences = [
        "123", "234", "345", "456",
        "567", "678", "789", "abc",
        "bcd", "cde", "xyz"
    ]

    features["has_sequence"] = int(
        any(seq in password.lower() for seq in sequences)
    )

    return features


# Test the feature extraction function
if __name__ == "__main__":

    sample_password = "Example@123"

    result = extract_features(sample_password)

    print("\nPASSWORD FEATURE EXTRACTION")
    print("---------------------------")

    for feature, value in result.items():
        print(f"{feature}: {value}")
