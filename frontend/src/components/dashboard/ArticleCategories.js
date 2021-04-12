import { Doughnut } from 'react-chartjs-2';
import {
  Box,
  Card,
  CardContent,
  CardHeader,
  Divider,
  Typography,
  colors,
  useTheme
} from '@material-ui/core';
import LaptopMacIcon from '@material-ui/icons/LaptopMac';
import PhoneIcon from '@material-ui/icons/Phone';
import TabletIcon from '@material-ui/icons/Tablet';
import { useQuery, gql, fromError } from '@apollo/client';

const query = gql`
query{
  categories{
    name,
    number
  }
}`;

const ArticleCategories = (props) => {
  const theme = useTheme();

  const { loading, error, data } = useQuery(query);

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error :(</p>;

  let colors_ = [
    colors.indigo[500],
    colors.red[600],
    colors.orange[600],
    colors.blue[600],
    colors.green[600],
    colors.cyan[600],
    colors.pink[600],
    colors.purple[600]
  ];

  let additionalCategoriesInfo = [];

    var valuesSum = 0;
    for (var i = 0; i < data.categories.length; i++){
      valuesSum += data.categories[i].number;
    }

    var values = []
    var labels = []
    for (var i = 0; i < data.categories.length; i++){
      var number = data.categories[i].number;
      var label = data.categories[i].name;

      values.push(number);
      labels.push(label);

      additionalCategoriesInfo.push({title: label, value: Math.round((number / valuesSum) * 100), color: colors_[i]});
    }

  const graphData = {
    datasets: [
      {
        data: values,
        backgroundColor: colors_,
        borderWidth: 8,
        borderColor: colors.common.white,
        hoverBorderColor: colors.common.white
      }
    ],
    labels: labels
  };

  const options = {
    animation: false,
    cutoutPercentage: 80,
    layout: { padding: 0 },
    legend: {
      display: false
    },
    maintainAspectRatio: false,
    responsive: true,
    tooltips: {
      backgroundColor: theme.palette.background.paper,
      bodyFontColor: theme.palette.text.secondary,
      borderColor: theme.palette.divider,
      borderWidth: 1,
      enabled: true,
      footerFontColor: theme.palette.text.secondary,
      intersect: false,
      mode: 'index',
      titleFontColor: theme.palette.text.primary
    }
  };  

  return (
    <Card {...props}>
      <CardHeader title="Kategorie článků" />
      <Divider />
      <CardContent>
        <Box
          sx={{
            height: 300,
            position: 'relative'
          }}
        >
          <Doughnut
            data={graphData}
            options={options}
          />
        </Box>
        <Box
          sx={{
            display: 'flex',
            justifyContent: 'center',
            pt: 2
          }}
        >
          {additionalCategoriesInfo.map(({
            color,
            title,
            value
          }) => (
            <Box
              key={title}
              sx={{
                p: 1,
                textAlign: 'center'
              }}
            >
              <Typography
                color="textPrimary"
                variant="body1"
              >
                {title}
              </Typography>
              <Typography
                style={{ color }}
                variant="h5"
              >
                {value}
                %
              </Typography>
            </Box>
          ))}
        </Box>
      </CardContent>
    </Card>
  );
};

export default ArticleCategories;
