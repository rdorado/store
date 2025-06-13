import { Routes } from '@angular/router';
import { AdminComponent } from './admin/admin.component';
import { StoreComponent } from './store/store.component';
import { CategoryComponent } from './admin/category/category.component';

export const routes: Routes = [
    { path: 'admin', component: AdminComponent },
    { path: 'admin/categories', component: CategoryComponent },
    { path: 'store', component: StoreComponent },
];
