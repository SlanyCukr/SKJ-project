import { Helmet } from 'react-helmet';
import {
  Box,
  Container,
  Grid
} from '@material-ui/core';
import NewArticles from 'src/components/dashboard/NewArticles';
import NewestArticles from 'src/components/dashboard/NewestArticles';
import MostFrequentAuthors from 'src/components/dashboard/MostFrequentAuthors';
import ArticleCommentGraph from 'src/components/dashboard/ArticleCommentGraph';
import TasksProgress from 'src/components/dashboard//TasksProgress';
import NewComments from 'src/components/dashboard/NewComments';
import AuthorsCount from 'src/components/dashboard/AuthorsCount';
import ArticleCategories from 'src/components/dashboard/ArticleCategories';

const Dashboard = () => {
  return(
  <>
    <Helmet>
      <title>SKJ projekt dashboard</title>
    </Helmet>
    <Box
      sx={{
        backgroundColor: 'background.default',
        minHeight: '100%',
        py: 3
      }}
    >
      <Container maxWidth={false}>
        <Grid
          container
          spacing={3}
        >
          <Grid
            item
            lg={3}
            sm={6}
            xl={3}
            xs={12}
          >
            <NewArticles />
          </Grid>
          <Grid
            item
            lg={3}
            sm={6}
            xl={3}
            xs={12}
          >
            <NewComments />
          </Grid>
          <Grid
            item
            lg={3}
            sm={6}
            xl={3}
            xs={12}
          >
            <TasksProgress />
          </Grid>
          <Grid
            item
            lg={3}
            sm={6}
            xl={3}
            xs={12}
          >
            <AuthorsCount sx={{ height: '100%' }} />
          </Grid>
          <Grid
            item
            lg={12}
            sm={24}
            xl={12}
            xs={48}
          >
            <ArticleCommentGraph />
          </Grid>
          <Grid
            item
            lg={8}
            md={12}
            xl={9}
            xs={12}
          >
            <ArticleCategories sx={{ height: '100%' }} />
          </Grid>
          <Grid
            item
            lg={4}
            md={6}
            xl={3}
            xs={12}
          >
            <MostFrequentAuthors sx={{ height: '100%' }} />
          </Grid>
          <Grid
            item
            lg={8}
            md={12}
            xl={9}
            xs={12}
          >
            <NewestArticles />
          </Grid>
        </Grid>
      </Container>
    </Box>
  </>
)};

export default Dashboard;
