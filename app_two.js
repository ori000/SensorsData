import express from 'express';
import { createClient } from '@supabase/supabase-js';
import morgan from 'morgan';
import bodyParser from 'body-parser';
import { seedTemperatures } from './seeder.js';

const app = express();

// Using morgan for logs
app.use(morgan('combined'));

app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

const supabase = createClient('https://frpruiluczkxupczcdnr.supabase.co', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZycHJ1aWx1Y3preHVwY3pjZG5yIiwicm9sZSI6ImFub24iLCJpYXQiOjE2OTc3MzI0NjgsImV4cCI6MjAxMzMwODQ2OH0.dLAM5fJwWS7iS7Th_XRAii6x9CsUOi4HNEUkSwth73Y')

app.get('/sensordata', async (req, res) => {
  const { data, error } = await supabase
    .from('SensorData')
    .select()
  res.send(data);
});

app.get('/sensordata/:id', async (req, res) => {
  const { data, error } = await supabase
    .from('SensorData')
    .select()
    .eq('id', req.params.id)
  res.send(data);
});

app.get('/locationdata', async (req, res) => {
  const location = req.query.location;

  console.log('Received location:', location);

  if (!location) {
    return res.status(400).send('Location parameter is required.');
  }

  try {
    const { data, error } = await supabase
      .from('SensorData')
      .select()
      .eq('location', location);

    console.log('Supabase Response:', data);

    if (error) {
      console.error(error);
      res.status(500).send('Internal Server Error');
    } else {
      res.send(data);
    }
  } catch (error) {
    console.error(error);
    res.status(500).send('Internal Server Error');
  }
});

app.get('/schedule', async (req, res) => {
  const { building, room, day, time } = req.query;

  const queryTime = parseInt(time, 10);

  if (!building || !room || !day || isNaN(queryTime)) {
    return res.status(400).send('All parameters (building, room, day, time) are required.');
  }

  try {
    const { data, error } = await supabase
      .from('PopulationData')
      .select('*')
      .eq('building', building)
      .eq('room', room)
      .eq(day, true)
      .lte('beginTime', queryTime)
      .gte('endTime', queryTime);

    if (error) {
      console.error(error);
      return res.status(500).send('Internal Server Error');
    }
    
    res.send(data);
  } catch (error) {
    console.error(error);
    res.status(500).send('Internal Server Error');
  }
});

app.post('/sensordata', async (req, res) => {
  const { error } = await supabase
    .from('SensorData')
    .insert({
      location: req.body.location,
      temperature: req.body.temperature,
    });
  if (error) {
    res.send(error);
  }
  res.send("Temperature data created!!");
});

app.put('/sensordata/:id', async (req, res) => {
  const { error } = await supabase
    .from('SensorData')
    .update({
      location: req.body.location,
      temperature: req.body.temperature,
    })
    .eq('id', req.params.id);
  if (error) {
    res.send(error);
  }
  res.send("Temperature data updated!!");
});

app.delete('/sensordata/:id', async (req, res) => {
  const { error } = await supabase
    .from('SensorData')
    .delete()
    .eq('id', req.params.id);
  if (error) {
    res.send(error);
  }
  res.send("Temperature data deleted!!");
});

app.post('/seed-sensordata', async (req, res) => {
    try {
      await seedTemperatures(); // Call the seeder function
      res.send('Temperature data seeded successfully!');
    } catch (error) {
      res.status(500).send('Error seeding temperature data.');
    }
  });


app.get('/', (req, res) => {
  res.send("Hello, I am working with temperature data using Supabase <3");
});

app.get('*', (req, res) => {
  res.send("Hello again, I am working with temperature data using Supabase to the moon and beyond <3");
});

app.listen(3000, () => {
  console.log(`> Ready on http://localhost:3000`);
});