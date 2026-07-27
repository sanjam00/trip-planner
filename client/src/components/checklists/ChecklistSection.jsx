// shown inside TripDetailPage, lists all checklists for that trip

import { useParams } from "react-router";
import { useAuth } from "../../context/AuthContext";
import { useEffect, useState } from "react";
import { apiFetch } from "../../api/api";

export default function ChecklistSection() {
  const { trip_id, checklist_id } = useParams();  // grabs trip_id from /trips/<trip_id>
  const { token } = useAuth();
  const [listData, setListData] = useState(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  // fetching from CheckListById
  // useEffect(() => {
  //   setLoading(true);
  //   apiFetch(`/trips/${trip_id}/checklists`, token)
  //     .then(data => {
  //       setListData(data);
  //       console.log(data);
  //     })
  //     .catch(err => {
  //       setError(err.message)
  //       console.error(err)
  //     })
  //     .finally(() => setLoading(false));
  // }, [trip_id, token])

  return (
    <div>
      <p>This is the checklist section component</p>

      {/* <h2>{listData.checklists[title]}</h2> */}
    </div>
  )
}