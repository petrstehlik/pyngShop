import { TestBed, inject } from '@angular/core/testing';

import { AdminManufacturerService } from './admin-manufacturer.service';

describe('AdminManufacturerService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [AdminManufacturerService]
    });
  });

  it('should ...', inject([AdminManufacturerService], (service: AdminManufacturerService) => {
    expect(service).toBeTruthy();
  }));
});
