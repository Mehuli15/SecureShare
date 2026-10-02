import os

from ml.anomaly_detector import analyze_file


TEST_DIR = os.path.dirname(__file__)


def create_test_file(filename, content):
    path = os.path.join(TEST_DIR, filename)

    with open(path, "w", encoding="utf-8") as file:
        file.write(content)

    return path


# ------------------------------------------------------------
# NORMAL FILES
# ------------------------------------------------------------

normal_files = [
    create_test_file(
        "report.pdf.txt",
        "This is a normal project report file."
    ),
    create_test_file(
        "assignment.txt",
        "This is a normal assignment document."
    ),
    create_test_file(
        "presentation.pptx.txt",
        "This is a normal presentation file."
    ),
]


# ------------------------------------------------------------
# UNUSUAL FILES
# ------------------------------------------------------------

unusual_files = [
    create_test_file(
        "x9K_random_839472.bin",
        "x"
    ),
    create_test_file(
        "random_839472_XYZ987654321.bin",
        "x"
    ),
    create_test_file(
        "VERY_LONG_RANDOM_FILENAME_839472_ABCXYZ_TEST_FILE.unknown",
        "x"
    ),
]


print("=" * 60)
print("ML ANOMALY DETECTOR EVALUATION")
print("=" * 60)


print("\nNORMAL FILES")
print("-" * 60)

for path in normal_files:
    result = analyze_file(path)

    print(
        f"{os.path.basename(path):50} "
        f"-> {result['status']:10} "
        f"score={result['score']:.4f}"
    )


print("\nUNUSUAL FILES")
print("-" * 60)

for path in unusual_files:
    result = analyze_file(path)

    print(
        f"{os.path.basename(path):50} "
        f"-> {result['status']:10} "
        f"score={result['score']:.4f}"
    )


print("\nEvaluation complete.")