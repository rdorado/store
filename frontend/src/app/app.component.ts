import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { BackendService } from '../services/backend.service';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, CommonModule],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss'
})
export class AppComponent {
  imageToShow: any;
  isImageLoading: boolean = false;
  constructor(private backend: BackendService) { 
  }
/*
  createImageFromBlob(image: Blob) {
    let reader = new FileReader();
    reader.addEventListener("load", () => {
       this.imageToShow = reader.result;
    }, false);
 
    if (image) {
       reader.readAsDataURL(image);
    }
 }
  
  getImageFromService() {
    this.isImageLoading = true;
    this.backend.getImage().subscribe({
      next: (data) => {
        console.log(data);
        this.createImageFromBlob(data);
        this.isImageLoading = false;
      },
      error: (error) => {
        this.isImageLoading = false;
        console.log(error);
      }
    });
  }

  getFileInfo() {
    this.backend.getFileInfo();
  }

*/
}