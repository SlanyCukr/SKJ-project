import { v4 as uuid } from 'uuid';
import moment from 'moment';
import {
  Box,
  Button,
  Card,
  CardHeader,
  Divider,
  IconButton,
  List,
  ListItem,
  ListItemAvatar,
  ListItemText
} from '@material-ui/core';
import PersonIcon from '@material-ui/icons/Person';
import { useQuery, gql, fromError } from '@apollo/client';

const query = gql`
query{
  mostFrequentAuthors{
    value,
    date
  }
}`;

function getCzechDateRepresentation(date){
  // heavily inspired by https://github.com/fprochazka/nette-components/blob/master/TimeAgoInWords/Helpers.php
  var parsedDate = new Date(date);
  var delta = Math.round(Math.abs(new Date() - parsedDate) / 60000);
  if (delta == 0) return "před okamžikem";
  if (delta == 1) return "před minutou";
  if (delta < 45) return "před " + delta + " minutami";
  if (delta < 90) return "před hodinou";
  if (delta < 1440) return "před " + Math.round(delta / 60) + " hodinami";
  if (delta < 2880) return "včera";
  if (delta < 43200) return "před " + Math.round(delta / 1440) + " dny";
	if (delta < 86400) return "před měsícem";
	if (delta < 525960) return "před " + Math.round(delta / 43200) + " měsíci";
	if (delta < 1051920) return "před rokem";
  return "před " + Math.round(delta / 525960) + " lety";
}

const MostFrequentAuthors = (props) => {
  const { loading, error, data } = useQuery(query);

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error :(</p>;

  var authors = [];
  for(var i = 0; i < data.mostFrequentAuthors.length; i++){
    authors.push({id: uuid(), name: data.mostFrequentAuthors[i].value, date: getCzechDateRepresentation(data.mostFrequentAuthors[i].date)});
  }

  return(
  <Card {...props}>
    <CardHeader
      subtitle={`${authors.length} celkem`}
      title="Nejčastější autoři"
    />
    <Divider />
    <List>
      {authors.map((authors, i) => (
        <ListItem
          divider={i < authors.length - 1}
          key={authors.id}
        >
          <PersonIcon />
          <ListItemText
            primary={authors.name}
            secondary={`poslední článek ${authors.date}`}
          />
          <IconButton
            edge="end"
            size="small"
          >
          </IconButton>
        </ListItem>
      ))}
    </List>
    <Divider />
    <Box
      sx={{
        display: 'flex',
        justifyContent: 'flex-end',
        p: 2
      }}
    >
    </Box>
  </Card>
)};

export default MostFrequentAuthors;
