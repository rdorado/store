import { Component, ElementRef, Input, OnInit, ViewChild } from "@angular/core";
import { BackendService } from "../../../services/backend.service";


@Component({
  selector: 'image',
  standalone: true,
  imports: [
  ],
  templateUrl: './image.component.html',
  styleUrl: './image.component.scss'
})
export class ImageComponent implements OnInit {
  @Input({ required: true }) id!: number;
  imageToShow: any;

  constructor(private backendService: BackendService) {
  }

  ngOnInit(): void {
    this.backendService.getImage(this.id).subscribe({
        next: result => this.createImageFromBlob(result)
    });
  }

  createImageFromBlob(image: Blob) {
   let reader = new FileReader();
   reader.addEventListener("load", () => {
      this.imageToShow = reader.result;
   }, false);

   if (image) {
      reader.readAsDataURL(image);
   }
}
}