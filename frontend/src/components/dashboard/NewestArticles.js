import moment from 'moment';
import { v4 as uuid } from 'uuid';
import PerfectScrollbar from 'react-perfect-scrollbar';
import {
  Box,
  Button,
  Card,
  CardHeader,
  Chip,
  Divider,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  TableSortLabel,
  Tooltip
} from '@material-ui/core';
import ArrowRightIcon from '@material-ui/icons/ArrowRight';
import { useQuery, gql, fromError } from '@apollo/client';

const query = gql`
query{
  newestArticles{
    link,
    header,
    category,
    createdOn,
    commentCount
  }
}`;

const NewestArticles = (props) => {
  const { loading, error, data } = useQuery(query);

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error :(</p>;

  var tableData = [];
  for(var i = 0; i < data.newestArticles.length; i++){
    var articleInfo = data.newestArticles[i];
    tableData.push({id: uuid(), link: articleInfo.link, header: articleInfo.header, category: articleInfo.category, createdOn: new Date(articleInfo.createdOn), commentCount: articleInfo.commentCount});
  }

  return(
  <Card {...props}>
    <CardHeader title="Nejnovější články" />
    <Divider />
    <PerfectScrollbar>
      <Box sx={{ minWidth: 800 }}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>
                Hlavička
              </TableCell>
              <TableCell>
                Kategorie
              </TableCell>
              <TableCell>
                Datum
              </TableCell>
              <TableCell>
                Počet komentářů
              </TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {tableData.map((tableData) => (
              <TableRow
                hover
                key={tableData.id}
              >
                <TableCell>
                  <a href={tableData.link} target="_blank">{tableData.header}</a>
                </TableCell>
                <TableCell>
                  {tableData.category}
                </TableCell>
                <TableCell>
                  {moment(tableData.createdOn).format('DD/MM/YYYY')}
                </TableCell>
                <TableCell>
                  <Chip
                    color="default"
                    label={tableData.commentCount}
                    size="small"
                  />
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </Box>
    </PerfectScrollbar>
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

export default NewestArticles;
