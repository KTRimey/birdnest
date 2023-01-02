import * as C from "@chakra-ui/react";
import { format } from "date-fns";

const PilotInfo = ({
  id,
  closest_approach,
  last_seen,
  name,
  phone,
  email,
}: {
  id: string;
  closest_approach: number;
  last_seen: string;
  name: string | null;
  phone: string | null;
  email: string | null;
}) => {
  return (
    <>
      <C.Td>
        <C.VStack fontSize="lg" alignItems="flex-start" spacing="0">
          <C.Text fontWeight="bold">{name ? name : ""}</C.Text>
          <C.Text fontSize="sm" opacity={0.6}>
            Drone ID: {id}
          </C.Text>
        </C.VStack>
      </C.Td>
      <C.Td fontSize="lg">
        <C.Text>{Math.round(closest_approach / 10) / 100} m</C.Text>
      </C.Td>
      <C.Td fontSize="lg">{format(new Date(last_seen), "h:mm a")}</C.Td>
      <C.Td>
        {name ? (
          <C.VStack fontSize="sm" alignItems="flex-end">
            <C.Text>{email}</C.Text>
            <C.Text>{phone}</C.Text>
          </C.VStack>
        ) : (
          "Pilot info not found"
        )}
      </C.Td>
    </>
  );
};

export default PilotInfo;
