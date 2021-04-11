import {
  Avatar,
  Box,
  Card,
  CardContent,
  Grid,
  Typography
} from '@material-ui/core';
import ArrowDownwardIcon from '@material-ui/icons/ArrowDownward';
import ArrowUpwardIcon from '@material-ui/icons/ArrowUpward';
import ArticleIcon from '@material-ui/icons/Article'
import { red } from '@material-ui/core/colors';
import { green } from '@material-ui/core/colors';
import { useQuery, gql, fromError } from '@apollo/client';

const query = gql`
query{
  newArticles{
    count,
    percent
  }
}`;

const NewArticles = (props) => {
  const { loading, error, data } = useQuery(query);

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
                {data.newArticles.percent}%
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
                {data.newArticles.percent}%
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
            NOVÉ ČLÁNKY
          </Typography>
          <Typography
            color="textPrimary"
            variant="h3"
          >
            {data.newArticles.count}
          </Typography>
        </Grid>
        <Grid item>
          <Avatar
            sx={{
              backgroundColor: red[600],
              height: 56,
              width: 56
            }}
          >
            <ArticleIcon />
          </Avatar>
        </Grid>
      </Grid>
      {data.newArticles.percent > 0 &&
      <Increase></Increase>
      }
      {data.newArticles.percent < 0 &&
      <Decrease></Decrease>
      }
    </CardContent>
  </Card>
)};

export default NewArticles;
