import { Component, OnInit, ViewEncapsulation, Input } from '@angular/core';
import { DatePipe } from '@angular/common';

@Component({
  selector: 'homework-detail',
  templateUrl: './homework-detail.component.html',
  styleUrls: ['./homework-detail.component.css'],
  encapsulation: ViewEncapsulation.None
})
export class HomeworkDetailComponent implements OnInit {
  @Input() homework: object;
  display: boolean;

  constructor() { }

  ngOnInit() {
    this.display = true;
  }

  eraseEntry() {
    this.display = false;
  }

}
