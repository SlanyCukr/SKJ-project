import {
  Avatar,
  Box,
  Card,
  CardContent,
  Grid,
  LinearProgress,
  Typography
} from '@material-ui/core';
import { orange } from '@material-ui/core/colors';
import InsertChartIcon from '@material-ui/icons/InsertChartOutlined';
import { useQuery, gql, fromError } from '@apollo/client';

const query = gql`
query{
  currentProgress
}`;

const TasksProgress = (props) => {
  const { loading, error, data } = useQuery(query, {pollInterval: localStorage.getItem('pollInterval') || 2000});

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error :(</p>;

  return(
  <Card
    sx={{ height: '100%' }}
    {...props}
  >
    <CardContent>
      <Grid
        container
        spacing={3}
        sx={{ justifyContent: 'space-between' }}
      >
        <Grid item>
          <Typography
            color="textSecondary"
            gutterBottom
            variant="h6"
          >
            PRŮBĚH SOUČASNÉHO SCRAPOVÁNÍ
          </Typography>
          <Typography
            color="textPrimary"
            variant="h3"
          >
            {data.currentProgress}%
          </Typography>
        </Grid>
        <Grid item>
          <Avatar
            sx={{
              backgroundColor: orange[600],
              height: 56,
              width: 56
            }}
          >
            <InsertChartIcon />
          </Avatar>
        </Grid>
      </Grid>
      <Box sx={{ pt: 3 }}>
        <LinearProgress
          value={data.currentProgress}
          variant="determinate"
        />
      </Box>
    </CardContent>
  </Card>
)};

export default TasksProgress;
