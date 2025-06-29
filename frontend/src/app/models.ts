export interface BlenderAsset {
  id: number;
  name: string;
  filename: string;
  details: string;
}

export interface Category {
  id: number;
  name: string;
  type: number;
}

export interface Asset {
  id: number;
  name: string;
  filename: string;
}