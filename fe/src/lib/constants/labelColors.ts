export interface LabelColors {
  [key: string]: string;
}

export const LABEL_COLORS: LabelColors = {
  // Detection Labels
  'bird': 'rgba(255, 223, 186, 0.8)',
  'cat': 'rgba(99, 102, 241, 0.8)',
  'dog': 'rgba(244, 63, 94, 0.8)',
  'horse': 'rgba(210, 180, 140, 0.8)',
  'sheep': 'rgba(128, 128, 128, 0.8)',
  'cow': 'rgba(255, 255, 0, 0.8)',
  'elephant': 'rgba(128, 128, 255, 0.8)',
  'bear': 'rgba(139, 69, 19, 0.8)',
  'zebra': 'rgba(0, 0, 0, 0.8)',
  'giraffe': 'rgba(255, 215, 0, 0.8)',

  // Classification Labels
  'Abyssinian': 'rgba(99, 102, 241, 0.8)',
  'Bengal': 'rgba(244, 63, 94, 0.8)',
  'Birman': 'rgba(99, 218, 99, 0.8)',
  'Bombay': 'rgba(255, 165, 0, 0.8)',
  'British Shorthair': 'rgba(75, 0, 130, 0.8)',
  'Egyptian Mau': 'rgba(0, 255, 255, 0.8)',
  'Maine Coon': 'rgba(255, 20, 147, 0.8)',
  'Persian': 'rgba(135, 206, 235, 0.8)',
  'Ragdoll': 'rgba(255, 192, 203, 0.8)',
  'Russian Blue': 'rgba(255, 255, 224, 0.8)',
  'Siamese': 'rgba(255, 255, 0, 0.8)',
  'Sphynx': 'rgba(210, 105, 30, 0.8)',
  'American Bulldog': 'rgba(255, 0, 0, 0.8)',
  'American Pit Bull Terrier': 'rgba(128, 0, 128, 0.8)',
  'Basset Hound': 'rgba(0, 128, 0, 0.8)',
  'Beagle': 'rgba(128, 128, 0, 0.8)',
  'Boxer': 'rgba(255, 165, 0, 0.8)',
  'Chihuahua': 'rgba(255, 192, 203, 0.8)',
  'English Cocker Spaniel': 'rgba(0, 255, 255, 0.8)',
  'English Setter': 'rgba(75, 0, 130, 0.8)',
  'German Shorthaired Pointer': 'rgba(99, 102, 241, 0.8)',
  'Great Pyrenees': 'rgba(244, 63, 94, 0.8)',
  'Havanese': 'rgba(255, 0, 255, 0.8)',
  'Japanese Chin': 'rgba(0, 128, 128, 0.8)',
  'Keeshond': 'rgba(245, 222, 179, 0.8)',
  'Leonberger': 'rgba(134, 1, 1, 0.8)',
  'Miniature Pinscher': 'rgba(192, 192, 192, 0.8)',
  'Newfoundland': 'rgba(255, 140, 0, 0.8)',
  'Pomeranian': 'rgba(255, 20, 147, 0.8)',
  'Pug': 'rgba(255, 192, 203, 0.8)',
  'Saint Bernard': 'rgba(139, 69, 19, 0.8)',
  'Samoyed': 'rgba(255, 250, 205, 0.8)',
  'Scottish Terrier': 'rgba(139, 0, 139, 0.8)',
  'Shiba Inu': 'rgba(255, 228, 181, 0.8)',
  'Staffordshire Bull Terrier': 'rgba(208, 227, 209, 0.8)',
  'Wheaten Terrier': 'rgba(255, 0, 255, 0.8)',
  'Yorkshire Terrier': 'rgba(128, 0, 128, 0.8)'
} as const;

export type LabelType = keyof typeof LABEL_COLORS;