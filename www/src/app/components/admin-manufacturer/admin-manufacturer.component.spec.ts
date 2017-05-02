import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { AdminManufacturerComponent } from './admin-manufacturer.component';

describe('AdminManufacturerComponent', () => {
  let component: AdminManufacturerComponent;
  let fixture: ComponentFixture<AdminManufacturerComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ AdminManufacturerComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AdminManufacturerComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
