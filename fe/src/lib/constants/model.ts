import { ModelType } from "@/types/modelType";
import { delay } from "@/utils/delay";

export const categories = [
  {
    id: "object-detection",
    title: "Object Detection",
    description: "Identify object positions with bounding boxes",
    image: "/images/object-detection.png",
    types: "with YOLO v5,8,11",
  },
  {
    id: "image-classification",
    title: "Image Classification",
    description: "Assign labels to the entire image",
    image: "/images/classification.png",
    types: "with YOLO v5,8,11",
  },
];

export const models = {
  "object-detection": [
    {
      id: "yolo-v5",
      name: "YOLO v5",
      image: "/images/yolo-v5.png",
      description: "Fast and accurate object detection",
      releaseDate: "Released in Jan 2021",
    },
    {
      id: "yolo-v8",
      name: "YOLO v8",
      image: "/images/yolo-v8.png",
      description: "Advanced object detection model",
      releaseDate: "Released in January 5th, 2023",
    },
    {
      id: "yolo-v11",
      name: "YOLO v11",
      image: "/images/yolo-v11.png",
      description: "Latest YOLO version",
      releaseDate: "Released at September 5th, 2024",
    },
  ],
  "image-classification": [
    {
      id: "resnet",
      name: "ResNet",
      image: "/images/resnet.png",
      description: "Deep residual learning",
      releaseDate: "Classic architecture",
    },
    {
      id: "yolo-v6",
      name: "YOLO v6",
      image: "/images/yolo-v6.png",
      description: "Optimized for classification",
      releaseDate: "Released in 2022",
    },
    {
      id: "yolo-v7",
      name: "YOLO v7",
      image: "/images/yolo-v7.png",
      description: "Enhanced classification",
      releaseDate: "Released in 2023",
    },
  ],
};
