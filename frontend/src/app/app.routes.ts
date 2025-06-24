import { Routes } from '@angular/router';
import { AdminComponent } from './admin/admin.component';
import { StoreComponent } from './store/store.component';
import { CategoryComponent } from './admin/category/category.component';
import { AssetComponent } from './admin/asset/asset.component';


export const routes: Routes = [
  { path: 'admin', component: AdminComponent },
  { path: 'admin/categories', component: CategoryComponent },
  { path: 'admin/asset', component: AssetComponent },
  { path: 'store', component: StoreComponent },
];
