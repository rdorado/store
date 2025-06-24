import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { CdkTableModule } from '@angular/cdk/table';
import { DataSource } from '@angular/cdk/collections';
import { BackendService } from '../../../services/backend.service';
import { Asset } from '../../models';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { BehaviorSubject, Observable } from 'rxjs';


@Component({
  selector: 'app-category',
  standalone: true,
  imports: [
    ReactiveFormsModule,
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
        console.log(this.form);
        this.backendService.createAsset(this.form.value).subscribe({
          next: asset => {
            console.log(asset);
            if(this.file) {
              const formData = new FormData();
              ///formData.append("asset_id", asset.id.toString());
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

  fetchData() {
    this.backendService.getAsset().subscribe({next: (asset) => {
      console.log(asset);
      this.dataSource = new AssetDataSource(asset);
    }})
  }

  clickNew() {
    this.displayTable = "none";
    this.displayForm = "block";
    this.formType = "insert";
  }

  clickEdit(asset: Asset) {
    console.log(asset);
    //this.form.setValue(asset);
    this.form.patchValue({
      name: asset.name,
      id: asset.id
    });
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