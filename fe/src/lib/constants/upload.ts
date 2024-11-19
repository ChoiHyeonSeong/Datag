export const ACCEPTED_FILE_TYPES = {
    "image/*": [".jpeg", ".jpg", ".png", ".gif"],
    "application/zip": [".zip"],
    "application/x-zip-compressed": [".zip"],
    "application/x-7z-compressed": [".7z"],
    "application/json": [".json"],
} as const;

export const ERROR_MESSAGES = {
    DUPLICATE_FILES: (files: string[]) =>
        `이미 업로드된 파일이 있습니다: ${files.join(", ")}`,
    MIXED_FILES: "압축 파일과 이미지 파일을 동시에 업로드하지 마세요",
    MULTIPLE_ZIP: "하나의 압축 파일만 올려주세요",
    INVALID_TYPE: "압축 파일과 이미지 파일 중 한 가지 타입만을 올려주세요.",
    UNSUPPORTED_TYPE: (files: string[]) =>
        `지원하지 않는 파일 형식입니다: ${files.join(", ")}`,
} as const;
