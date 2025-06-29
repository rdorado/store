import { Component, OnInit } from '@angular/core';
import { Asset, Category } from '../models';
import { BackendService } from '../../services/backend.service';
import { ImageComponent } from '../shared/image/image.component';

@Component({
  selector: 'app-store',
  standalone: true,
  imports: [
    ImageComponent
  ],
  templateUrl: './store.component.html',
  styleUrl: './store.component.scss'
})
export class StoreComponent implements OnInit{

  categories: Category[] = [];
  selectedCategory: Category|undefined;
  assets: Asset[] = [];

  constructor(private backendService: BackendService) {
  }

  ngOnInit(): void {
    this.backendService.getCategoriesByType(1).subscribe({
      next:categories => {
        this.categories = categories;
        this.selectedCategory = this.categories.at(0);
      }
    });
    this.backendService.getAsset().subscribe({
      next: assets => {
        this.assets = assets;
      }
    });
  }
}
