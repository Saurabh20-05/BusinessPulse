from fastapi import HTTPException, UploadFile, status


def validate_csv_file(file: UploadFile) -> None:
    """
    Validate the uploaded CSV file before processing.
    """

    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No file selected.",
        )

    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only CSV files are supported.",
        )