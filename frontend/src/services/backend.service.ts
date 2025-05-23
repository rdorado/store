import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { BlenderAsset } from '../app/models';

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

  getAssetList(): Observable<BlenderAsset[]> {
    return this.httpClient.get<BlenderAsset[]>(this.API_URL+"/blender_asset/get");
  }

  getImage(): Observable<Blob> {
    return this.httpClient.get(this.API_URL+"/img", { responseType: 'blob' });
  }

  getFileInfo() {
    return this.httpClient.get(this.API_URL+"/info")
      .subscribe({
        next: (result) => console.log(result),
        error: (error) => console.log(error)
      });
  }

  submitFile(formData: FormData): Observable<any>{
    return this.httpClient.post(this.API_URL+"/blender_asset", formData);
  }

  deleteBlenderAsset(asset_id: number): Observable<any>{
    console.log(`${this.API_URL}/blender_asset/${asset_id}`);
    return this.httpClient.delete(`${this.API_URL}/blender_asset/${asset_id}`);
  }

  createAsset(value: BlenderAsset) {
    return this.httpClient.post(`${this.API_URL}/blender_asset`, value);
  }
}
