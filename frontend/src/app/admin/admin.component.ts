import { Component, OnInit } from '@angular/core';
import { BackendService } from '../../services/backend.service';
import { BlenderAsset } from '../models';
import {FormBuilder, FormControl, FormGroup, ReactiveFormsModule, Validators} from '@angular/forms';

@Component({
  selector: 'app-admin',
  standalone: true,
  imports: [
    ReactiveFormsModule,
  ],
  templateUrl: './admin.component.html',
  styleUrl: './admin.component.scss'
})
export class AdminComponent implements OnInit{
  assets: any[] = [];
  form: FormGroup;

  constructor(private backendService: BackendService, private fb: FormBuilder){
    this.form = this.fb.group({
      name: ['', Validators.required],
    });
  }

  ngOnInit(): void {
    this.updateAssetsList();
  }

  updateAssetsList() {
    this.backendService.getAssetList().subscribe({
      next: result => {console.log(result); this.assets = result;}
    });
  }

  createDatabase() {
    this.backendService.createDatabase();
  }

  delete_blender_asset(event: Event, asset_id: number){
    event.preventDefault();
    this.backendService.deleteBlenderAsset(asset_id)
      .subscribe(_ => {
        this.updateAssetsList();
      });
  }

  get_blender_asset_details(event: Event, asset: BlenderAsset){
    event.preventDefault();
    asset.details = "test";
  }

  onFileSelected(event: any) {
    const file: File = event.target.files[0]
    if (file) {
      const formData = new FormData();
      formData.append("blender_file", file);
      this.backendService.submitFile(formData)
        .subscribe(_ => {
          this.updateAssetsList();
        });
    }
  }

  onSubmit(){
    if (this.form.valid) {
      this.backendService.createAsset(this.form.value).subscribe(_=>_);
      console.log('Form submitted:', this.form.value);
    }
  }
}
