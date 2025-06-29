import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { Asset, Category } from '../app/models';

@Injectable({
  providedIn: 'root'
})
export class BackendService {

  API_URL: string = "http://localhost:8000";

  constructor(private httpClient: HttpClient) { }

  createDatabase(){
    return this.httpClient.get(this.API_URL+"/db/create")
      .subscribe({next: result => console.log(result)});
  }

  getImage(id: number): Observable<Blob> {
    return this.httpClient.get(`${this.API_URL}/img/?id=${id}`, { responseType: 'blob' });
  }

  getFileInfo() {
    return this.httpClient.get(this.API_URL+"/info")
      .subscribe({
        next: (result) => console.log(result),
        error: (error) => console.log(error)
      });
  }

  submitFile(asset_id: number, formData: FormData): Observable<any>{
    return this.httpClient.post(`${this.API_URL}/blender_asset/${asset_id}`, formData);
  }

  deleteBlenderAsset(asset_id: number): Observable<any>{
    console.log(`${this.API_URL}/blender_asset/${asset_id}`);
    return this.httpClient.delete(`${this.API_URL}/blender_asset/${asset_id}`);
  }

  /**
   *  Category
   */
  createCategory(value: Category) {
    return this.httpClient.post(`${this.API_URL}/category`, value);
  }

  updateCategory(value: Category) {
    return this.httpClient.put(`${this.API_URL}/category`, value);
  }

  deleteCategory(value: Category) {
    return this.httpClient.delete(`${this.API_URL}/category/${value.id}`);
  }

  getCategories() {
    return this.httpClient.get<Category[]>(`${this.API_URL}/category`);
  }

  getCategoriesByType(type: number) {
    return this.httpClient.get<Category[]>(`${this.API_URL}/category/type/${type}`);
  }

  /**
   *  Asset
   */
  createAsset(value: Asset): Observable<Asset> {
    return this.httpClient.post<Asset>(`${this.API_URL}/asset`, value);
  }

  updateAsset(value: Asset) {
    return this.httpClient.put(`${this.API_URL}/asset`, value);
  }

  deleteAsset(value: Asset) {
    return this.httpClient.delete(`${this.API_URL}/asset/${value.id}`);
  }

  getAsset() {
    return this.httpClient.get<Asset[]>(`${this.API_URL}/asset`);
  }

  getAssetCategories(asset: Asset) {
    return this.httpClient.get<Category[]>(`${this.API_URL}/asset_categories/${asset.id}`);
  }

  addCategoryToAsset(asset: Asset, categoryId: number) {
    return this.httpClient.put<Category[]>(`${this.API_URL}/asset_categories/${categoryId}`, asset);
  }

  removeCategoryFromAsset(asset: Asset, categoryId: number) {
    const options = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json',
      }),
      body: JSON.stringify(asset),
    };
    return this.httpClient.delete<Category[]>(`${this.API_URL}/asset_categories/${categoryId}`, options);
  }
}
