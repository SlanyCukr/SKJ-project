import { Helmet } from 'react-helmet';
import { Box, Container } from '@material-ui/core';
import Settings from 'src/components/settings/Settings';

const SettingsView = () => (
  <>
    <Helmet>
      <title>Nastavení | SKJ dashboard</title>
    </Helmet>
    <Box
      sx={{
        backgroundColor: 'background.default',
        minHeight: '100%',
        py: 3
      }}
    >
      <Container maxWidth="lg">
        <Box sx={{ pt: 3 }}>
          <Settings />
        </Box>
      </Container>
    </Box>
  </>
);

export default SettingsView;
