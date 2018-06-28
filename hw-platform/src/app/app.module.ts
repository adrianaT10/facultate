import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from "@angular/common/http";
import { NgModule } from '@angular/core';


import { AppComponent } from './app.component';
import { CourseService } from "./course.service";
import { HomeworkDetailComponent } from './homework-detail/homework-detail.component';


@NgModule({
  declarations: [
    AppComponent,
    HomeworkDetailComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule
  ],
  providers: [CourseService],
  bootstrap: [AppComponent]
})
export class AppModule { }
