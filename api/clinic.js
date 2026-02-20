// Serverless function: /api/clinic.json → /api/clinic
// Returns machine-readable clinic facts for AI agents.

const data = {
  "name": "Classic Vision Care",
  "url": "https://classicvisioncare.com",
  "founded": 1998,
  "rating": { "value": 4.7, "count": 756, "source": "Google Reviews" },
  "booking_url": "https://classicvisioncare.com/book-now/",
  "insurance_url": "https://classicvisioncare.com/insurance/",
  "locations": [
    {
      "name": "Classic Vision Care – Kennesaw",
      "slug": "kennesaw",
      "address": {
        "street": "1615 Ridenour Blvd Suite 201",
        "city": "Kennesaw",
        "state": "GA",
        "zip": "30152",
        "country": "US"
      },
      "phone": "(770) 499-2020",
      "fax": "(770) 499-2021",
      "geo": { "lat": 34.0285, "lng": -84.6155 },
      "page_url": "https://classicvisioncare.com/eye-doctor-kennesaw-ga/",
      "booking_url": "https://classicvisioncare.com/book-now/?location=kennesaw",
      "hours": {
        "monday": "closed",
        "tuesday": "09:00–18:00",
        "wednesday": "08:00–17:00",
        "thursday": "09:00–18:00",
        "friday": "08:00–17:00",
        "saturday": "10:00–14:00",
        "sunday": "closed"
      }
    },
    {
      "name": "Classic Vision Care – East Cobb",
      "slug": "eastcobb",
      "address": {
        "street": "3535 Roswell Rd Suite 8",
        "city": "Marietta",
        "state": "GA",
        "zip": "30062",
        "country": "US"
      },
      "phone": "(678) 560-8065",
      "fax": "(678) 560-8066",
      "geo": { "lat": 33.9365, "lng": -84.4483 },
      "page_url": "https://classicvisioncare.com/eye-doctor-marietta/",
      "booking_url": "https://classicvisioncare.com/book-now/?location=eastcobb",
      "hours": {
        "monday": "08:00–17:00",
        "tuesday": "09:00–18:00",
        "wednesday": "08:00–17:00",
        "thursday": "09:00–18:00",
        "friday": "closed",
        "saturday": "closed",
        "sunday": "closed"
      }
    }
  ],
  "doctors": [
    {
      "name": "Dr. Mital Patel, OD",
      "title": "Doctor of Optometry",
      "role": "Founder",
      "specialties": ["Dry eye treatment", "Specialty contact lenses"],
      "page_url": "https://classicvisioncare.com/dr-mital-patel-od/"
    },
    {
      "name": "Dr. Bhumi Patel, OD",
      "title": "Doctor of Optometry",
      "specialties": ["Pediatric eye care", "Myopia control"],
      "page_url": "https://classicvisioncare.com/dr-bhumi-patel-od/"
    }
  ],
  "services": [
    { "name": "Comprehensive Eye Exams", "url": "https://classicvisioncare.com/comprehensive-eye-exams/" },
    { "name": "Contact Lens Exams", "url": "https://classicvisioncare.com/contact-lens-exams/" },
    { "name": "Diabetic Eye Exams", "url": "https://classicvisioncare.com/diabetic-eye-exam/" },
    { "name": "Pediatric Eye Care", "url": "https://classicvisioncare.com/pediatric-eye-care/" },
    { "name": "Dry Eye Treatment", "url": "https://classicvisioncare.com/dry-eye-treatment/" },
    { "name": "IPL Therapy", "url": "https://classicvisioncare.com/dry-eye-treatment-intense-pulsed-light/" },
    { "name": "Radio Frequency Treatment", "url": "https://classicvisioncare.com/dry-eye-treatment-radio-frequency/" },
    { "name": "BlephEx", "url": "https://classicvisioncare.com/dry-eye-treatment-blephex/" },
    { "name": "Myopia Control", "url": "https://classicvisioncare.com/myopia-control/" },
    { "name": "MiSight Lenses", "url": "https://classicvisioncare.com/misight-lenses-for-myopia-control/" },
    { "name": "Ortho-K Lenses", "url": "https://classicvisioncare.com/ortho-k-lenses-for-myopia-control/" },
    { "name": "Eyeglasses", "url": "https://classicvisioncare.com/eyeglasses/" },
    { "name": "Sunglasses", "url": "https://classicvisioncare.com/sunglasses/" },
    { "name": "Contact Lenses", "url": "https://classicvisioncare.com/contact-lenses/" },
    { "name": "Specialty Contact Lenses", "url": "https://classicvisioncare.com/specialty-contact-lenses/" },
    { "name": "Scleral Lenses", "url": "https://classicvisioncare.com/scleral-lenses-atlanta/" },
    { "name": "Keratoconus Contacts", "url": "https://classicvisioncare.com/keratoconus-contacts/" }
  ],
  "conditions_treated": [
    { "name": "Glaucoma", "url": "https://classicvisioncare.com/glaucoma/" },
    { "name": "Macular Degeneration", "url": "https://classicvisioncare.com/macular-degeneration/" },
    { "name": "Astigmatism", "url": "https://classicvisioncare.com/astigmatism/" },
    { "name": "Eye Allergies", "url": "https://classicvisioncare.com/allergies/" },
    { "name": "Blepharitis", "url": "https://classicvisioncare.com/blepharitis/" },
    { "name": "Presbyopia", "url": "https://classicvisioncare.com/presbyopia/" },
    { "name": "Myopia", "url": "https://classicvisioncare.com/myopia-control/" }
  ],
  "insurance_accepted": [
    "VSP", "EyeMed", "Spectera",
    "Blue Cross Blue Shield", "Aetna", "Cigna", "United Healthcare",
    "Medicare", "Medicaid"
  ],
  "social_profiles": [
    { "platform": "Facebook", "url": "https://www.facebook.com/CVCGlasses/" },
    { "platform": "Instagram", "url": "https://www.instagram.com/classic_vision_care/" },
    { "platform": "Yelp (Kennesaw)", "url": "https://www.yelp.com/biz/classic-vision-care-kennesaw-kennesaw-2" },
    { "platform": "Yelp (East Cobb)", "url": "https://www.yelp.com/biz/classic-vision-care-east-cobb-marietta-3" },
    { "platform": "Apple Maps", "url": "https://maps.apple.com/place?place-id=IF88A2D772D41FED" },
    { "platform": "Google Maps (Kennesaw)", "url": "https://www.google.com/maps?cid=766182488100234452" },
    { "platform": "Google Maps (East Cobb)", "url": "https://www.google.com/maps?cid=8257995811434454820" }
  ]
};

export default function handler(req, res) {
  res.setHeader("Content-Type", "application/json; charset=utf-8");
  res.setHeader("Cache-Control", "public, max-age=3600");
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.status(200).json(data);
}
