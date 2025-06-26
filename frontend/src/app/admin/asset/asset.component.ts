import { Component, OnInit } from '@angular/core';
import {
  FormBuilder,
  FormGroup,
  FormsModule,
  ReactiveFormsModule,
  Validators,
} from '@angular/forms';
import { CdkTableModule } from '@angular/cdk/table';
import { DataSource } from '@angular/cdk/collections';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { BehaviorSubject, Observable } from 'rxjs';

import { BackendService } from '../../../services/backend.service';
import { Asset, Category } from '../../models';

@Component({
  selector: 'app-category',
  standalone: true,
  imports: [
    ReactiveFormsModule,
    FormsModule,
    CdkTableModule,
    CommonModule,
    RouterModule,
  ],
  templateUrl: './asset.component.html',
  styleUrl: './asset.component.scss'
})
export class AssetComponent implements OnInit {
  displayTable: string = "flex";
  displayForm: string = "none";
  formType: string = ""
  form: FormGroup;
  displayedColumns: string[] = ['name', 'filename', 'options'];
  dataSource: DataSource<Asset> = new AssetDataSource([]);
  file: File|null = null;

  /* Asset categories */
  categories: Category[] = [];
  availableCategories: Category[] = [];
  assetCategories: Category[] = [];
  assetCategoryId: number|undefined;
  selectedAsset: Asset|undefined;

  constructor(private backendService: BackendService, private fb: FormBuilder){
    this.form = this.fb.group({
      id: [],
      name: ['', Validators.required],
      filename: ['', Validators.required],
    });
  }

  ngOnInit(): void {
    this.fetchData();
  }

  onSubmit(){
    if (this.form.valid) {
      if (this.formType === "insert") {
        this.backendService.createAsset(this.form.value).subscribe({
          next: asset => {
            if(this.file) {
              const formData = new FormData();
              formData.append("blender_file", this.file);
              this.backendService.submitFile(asset.id, formData).subscribe({
                next: _=>_,
                error: e => console.log(e)
              });
            }
            this.clickCancelForm();
            this.form.reset();
            this.fetchData();
          },
          error: e => console.log(e)
        });
      }
      else if (this.formType === "update") {
        this.backendService.updateAsset(this.form.value).subscribe({
          next: _ => {
            this.clickCancelForm();
            this.form.reset();
            this.fetchData();
          },
          error: e => console.log(e)
        });
      }
    }
  }

  addCategory() {
    if (this.selectedAsset != null && this.assetCategoryId != null){
      this.backendService.addCategoryToAsset(this.selectedAsset, this.assetCategoryId).subscribe({
        next: _ => {
          if(this.selectedAsset != null) {
            this.updateAssetCategories(this.selectedAsset);
          }
        }
      });
    }
  }

  removeCategory(categoryId: number) {
    if (this.selectedAsset != null) {
        this.backendService.removeCategoryFromAsset(this.selectedAsset, categoryId).subscribe({
        next: _ => {
          if(this.selectedAsset != null) {
            this.updateAssetCategories(this.selectedAsset);
          }
        }
      });
    }
  }

  updateAssetCategories(asset: Asset) {
    this.backendService.getAssetCategories(asset).subscribe({
      next: categories => {
        this.assetCategories = categories;
        this.availableCategories = this.categories.filter(cat1 => {
          return !this.assetCategories.some(cat2 => cat1.id === cat2.id);
        });
      }
    });
  }

  fetchData() {
    this.backendService.getAsset().subscribe({next: (asset) => {
      this.dataSource = new AssetDataSource(asset);
    }});
    this.backendService.getCategories().subscribe({next: (categories) => {
      this.categories = categories;
    }});
  }

  clickNew() {
    this.displayTable = "none";
    this.displayForm = "block";
    this.formType = "insert";
  }

  clickEdit(asset: Asset) {
    this.form.patchValue({
      name: asset.name,
      id: asset.id
    });
    this.updateAssetCategories(asset);
    this.selectedAsset = asset;
    this.displayTable = "none";
    this.displayForm = "block";
    this.formType = "update";
  }

  clickDelete(asset: Asset) {
    this.backendService.deleteAsset(asset).subscribe(_=> this.fetchData());
  }

  clickCancelForm() {
    this.displayTable = "flex";
    this.displayForm = "none";
    this.formType = "";
    this.form.reset();
  }

  onFileSelected(event: any) {
    if (event.target.files && event.target.files[0])
    {
      this.file = event.target.files[0];
      const reader = new FileReader();
      //console.log(event);
      /*reader.onload = () => {
        //this.form.controls[].setValue(event.target.files[0]);
        this.form.patchValue({file: event.target.files[0]})
      };*/
      //
      reader.onload = () => {
        //this.form.patchValue({file: event.target.files[0]});
      }
      reader.readAsDataURL(event.target.files[0]);
    }
    /*const file: File = event.target.files[0];
    if (file) {
      const formData = new FormData();
      formData.append("blender_file", file);
      this.backendService.submitFile(formData)
        .subscribe(_ => {
          //this.updateAssetsList();
        });
    }*/
  }
}

class AssetDataSource extends DataSource<Asset> {
  data: BehaviorSubject<Asset[]>;
  
  constructor(data: Asset[]) {
    super();
    this.data = new BehaviorSubject<Asset[]>(data);
  }
  
  connect(): Observable<Asset[]> {
    return this.data;
  }

  disconnect() {}
}
