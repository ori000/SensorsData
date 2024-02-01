import { createClient } from '@supabase/supabase-js';
import faker from 'faker';

const supabase = createClient('https://frpruiluczkxupczcdnr.supabase.co', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZycHJ1aWx1Y3preHVwY3pjZG5yIiwicm9sZSI6ImFub24iLCJpYXQiOjE2OTc3MzI0NjgsImV4cCI6MjAxMzMwODQ2OH0.dLAM5fJwWS7iS7Th_XRAii6x9CsUOi4HNEUkSwth73Y')

export async function seedTemperatures() {
  const temperatureData = [];

  // Generate 500 random temperature values and locations
  for (let i = 0; i < 500; i++) {
    const location = faker.random.arrayElement(['Living Room', 'Bedroom', 'Kitchen', 'Office']);
    const temperature = faker.datatype.number({ min: -10, max: 40, precision: 0.1 });
    const air_quality = faker.random.arrayElement(['healthy', 'unhealthy', 'mediocre']);
    const population = faker.datatype.number({ min: 1, max: 100 });
    const humidity = faker.datatype.number({ min: 10, max: 90, precision: 0.1 });

    temperatureData.push({ location, temperature, air_quality, population, humidity });
  }

  // Insert temperature data into the Supabase table
  const { data, error } = await supabase.from('SensorData').insert(temperatureData);

  if (error) {
    console.error('Error seeding temperatures:', error);
  } else {
    console.log('Temperatures seeded successfully!');
  }
}