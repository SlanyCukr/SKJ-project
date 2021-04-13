import {
  Avatar,
  Box,
  Card,
  CardContent,
  Grid,
  Typography
} from '@material-ui/core';
import CommentIcon from '@material-ui/icons/Comment';
import ArrowDownwardIcon from '@material-ui/icons/ArrowDownward';
import ArrowUpwardIcon from '@material-ui/icons/ArrowUpward';
import { red } from '@material-ui/core/colors';
import { green } from '@material-ui/core/colors';
import { useQuery, gql, fromError } from '@apollo/client';

const query = gql`
query{
  newComments{
    count,
    percent
  }
}`;

const NewComments = (props) => {
  const { loading, error, data } = useQuery(query, {pollInterval: localStorage.getItem('pollInterval') || 2000});

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error :(</p>;

  function Increase(props){
    return(
  <Box
          sx={{
            pt: 2,
            display: 'flex',
            alignItems: 'center'
          }}
        >
          <ArrowUpwardIcon sx={{ color: green[900] }} />
          <Typography
            sx={{
              color: green[900],
              mr: 1
            }}
            variant="body2"
          >
              {data.newComments.percent}%
          </Typography>
          <Typography
            color="textSecondary"
            variant="caption"
          >
            Oproti předchozímu dni
          </Typography>
        </Box>
    )
  }
  
  function Decrease(props){
    return(
  <Box
          sx={{
            pt: 2,
            display: 'flex',
            alignItems: 'center'
          }}
        >
          <ArrowDownwardIcon sx={{ color: red[900] }} />
          <Typography
            sx={{
              color: red[900],
              mr: 1
            }}
            variant="body2"
          >
              {data.newComments.percent}%
          </Typography>
          <Typography
            color="textSecondary"
            variant="caption"
          >
            Oproti předchozímu dni
          </Typography>
        </Box>
    )
  }

  return(
  <Card {...props}>
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
            NOVÉ KOMENTÁŘE
          </Typography>
          <Typography
            color="textPrimary"
            variant="h3"
          >
            {data.newComments.count}
          </Typography>
        </Grid>
        <Grid item>
          <Avatar
            sx={{
              backgroundColor: green[600],
              height: 56,
              width: 56
            }}
          >
            <CommentIcon />
          </Avatar>
        </Grid>
      </Grid>
      {data.newComments.percent > 0 &&
      <Increase></Increase>
      }
      {data.newComments.percent < 0 &&
      <Decrease></Decrease>
      }
    </CardContent>
  </Card>
)};

export default NewComments;
