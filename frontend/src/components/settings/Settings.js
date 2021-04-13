import { useState } from 'react';
import {
  Box,
  Button,
  Card,
  CardContent,
  CardHeader,
  Divider,  
  TextField
} from '@material-ui/core';

const Settings = (props) => {
  const [values, setValues] = useState({
    urlGraphQL: localStorage.getItem('urlGraphQL') || "http://localhost:5001/graphql",
    pollInterval: localStorage.getItem('pollInterval') || 2000,
    pollIntervalCostly: localStorage.getItem('pollIntervalCostly') || 5000,
  });

  const handleChange = (event) => {
    setValues({
      ...values,
      [event.target.name]: event.target.value
    });
  };

  function updateConfig(){
    localStorage.setItem('urlGraphQL', values.urlGraphQL);
    localStorage.setItem('pollInterval', values.pollInterval);
    localStorage.setItem('pollIntervalCostly', values.pollIntervalCostly);
  }

  return (
    <form {...props}>
      <Card>
        <CardHeader
          title="Nastavení"
        />
        <Divider />
        <CardContent>
          <TextField
            fullWidth
            label="URL GraphQL serveru"
            margin="normal"
            name="urlGraphQL"
            onChange={handleChange}
            type="text"
            value={values.urlGraphQL}
            variant="outlined"
          />
          <TextField
            fullWidth
            label="Prodleva pro aktualizaci (ms)"
            margin="normal"
            name="pollInterval"
            onChange={handleChange}
            type="number"
            value={values.pollInterval}
            variant="outlined"
            InputProps={{
              inputProps: { 
                  max: 10000, min: 2000
              }
          }}
          />
          <TextField
            fullWidth
            label="Prodleva pro aktualizaci - costly operace (ms)"
            margin="normal"
            name="pollIntervalCostly"
            onChange={handleChange}
            type="number"
            value={values.pollIntervalCostly}
            variant="outlined"
            InputProps={{
              inputProps: { 
                  max: 20000, min: 5000
              }
          }}
          />
        </CardContent>
        <Divider />
        <Box
          sx={{
            display: 'flex',
            justifyContent: 'flex-end',
            p: 2
          }}
        >
          <Button
            color="primary"
            variant="contained"
            onClick={updateConfig}
          >
            Aktualizovat nastavení
          </Button>
        </Box>
      </Card>
    </form>
  );
};

export default Settings;
