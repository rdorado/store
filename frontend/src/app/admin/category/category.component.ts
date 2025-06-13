import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { CdkTableModule } from '@angular/cdk/table';
import { DataSource } from '@angular/cdk/collections';
import { BackendService } from '../../../services/backend.service';
import { Category } from '../../models';
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
  templateUrl: './category.component.html',
  styleUrl: './category.component.scss'
})
export class CategoryComponent implements OnInit {
  displayTable: string = "flex";
  displayForm: string = "none";
  formType: string = ""
  form: FormGroup;
  displayedColumns: string[] = ['name', 'options'];
  dataSource: DataSource<Category> = new CategoryDataSource([]);

  constructor(private backendService: BackendService, private fb: FormBuilder){
    this.form = this.fb.group({
      id: [],
      name: ['', Validators.required],
    });
  }

  ngOnInit(): void {
    this.fetchData();
  }

  onSubmit(){
    if (this.form.valid) {
      if (this.formType === "insert") {
        this.backendService.createCategoty(this.form.value).subscribe(_=> {
          this.clickCancelForm();
          this.form.reset();
          this.fetchData();
        });
      }
      else if (this.formType === "update") {
        this.backendService.updateCategoty(this.form.value).subscribe(_=> {
          this.clickCancelForm();
          this.form.reset();
          this.fetchData();
        });
      }
    }
  }

  fetchData() {
    this.backendService.getCategories().subscribe({next: (categories) => {
      this.dataSource = new CategoryDataSource(categories);
    }})
  }

  clickNewCategory() {
    this.displayTable = "none";
    this.displayForm = "block";
    this.formType = "insert";
  }

  clickEditCategory(category: Category) {
    this.form.setValue(category);
    this.displayTable = "none";
    this.displayForm = "block";
    this.formType = "update";
  }

  clickDeleteCategory(category: Category) {
    this.backendService.deleteCategory(category).subscribe(_=> this.fetchData());
  }

  clickCancelForm() {
    this.displayTable = "flex";
    this.displayForm = "none";
    this.formType = "";
  }
}

class CategoryDataSource extends DataSource<Category> {
  data: BehaviorSubject<Category[]>;
  
  constructor(data: Category[]) {
    super();
    this.data = new BehaviorSubject<Category[]>(data);
  }
  
  connect(): Observable<Category[]> {
    return this.data;
  }

  disconnect() {}
}