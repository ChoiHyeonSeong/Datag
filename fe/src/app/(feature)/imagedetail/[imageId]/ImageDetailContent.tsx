import { loadImageDetail } from "@/api/detail/loadImageDetail";
import ImageDetailClient from "./imageDetailClient";
import {
    isClassificationPrediction,
    isDetectionPrediction,
} from "@/types/metadata";

export async function ImageDetailContent({
    params,
}: {
    params: { imageId: string };
}) {
    const imageId = params.imageId;
    const data = await loadImageDetail(imageId);

    if (!data.data) {
        throw new Error("Data is undefined");
    }

    const aiResult = data.data.metadata?.aiResults?.[0];
    const prediction = aiResult?.predictions?.[0];

    const detections =
        aiResult?.task === "det" && isDetectionPrediction(prediction)
            ? prediction.detections
            : [];

    const initialUserAuthorities =
        data.data.access_control?.users?.map((user) => ({
            user_id: user.uid,
            user_name: user.name,
            department_name: user.department_name,
        })) || [];

    const initialDepartmentAuthorities =
        data.data.access_control?.departments || [];

    const initialTags = prediction?.tags || [];

    const classes =
        aiResult?.task === "det" && isDetectionPrediction(prediction)
            ? prediction.detections.map((detection) => detection.prediction)
            : aiResult?.task === "cls" && isClassificationPrediction(prediction)
            ? [prediction.prediction]
            : [];

    const metadata = data.data.metadata?.metadata || {
        branch: "",
        process: "",
        location: "",
        equipmentId: "",
        createdAt: "",
    };

    const imageSrc = data.data.metadata?.fileList?.[0] || "";

    return (
        <ImageDetailClient
            imageId={imageId}
            imageIdx={1}
            initialUserAuthorities={initialUserAuthorities}
            initialDepartmentAuthorities={initialDepartmentAuthorities}
            initialTags={initialTags}
            classes={classes}
            imageSrc={imageSrc}
            metadata={metadata}
            detections={detections}
        />
    );
}
