import {
  Avatar,
  Card,
  CardContent,
  Grid,
  Typography
} from '@material-ui/core';
import { indigo } from '@material-ui/core/colors';
import InfoIcon from '@material-ui/icons/Info';
import { useQuery, gql, fromError } from '@apollo/client';

const query = gql`
query{
  articlesCount
}`;

const ArticlesCount = (props) => {
  const { loading, error, data } = useQuery(query);

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error :(</p>;


  return (
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
            CELKOVÝ POČET ČLÁNKŮ
          </Typography>
          <Typography
            color="textPrimary"
            variant="h3"
          >
            {data.articlesCount}
          </Typography>
        </Grid>
        <Grid item>
          <Avatar
            sx={{
              backgroundColor: indigo[600],
              height: 56,
              width: 56
            }}
          >
            <InfoIcon />
          </Avatar>
        </Grid>
      </Grid>
    </CardContent>
  </Card>
)};

export default ArticlesCount;