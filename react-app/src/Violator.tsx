import * as C from "@chakra-ui/react";
import { format } from "date-fns";

const Violator = ({
  id,
  closest_approach,
  closest_approach_time,
  first_name,
  last_name,
  phone,
  email,
}: {
  id: string;
  closest_approach: number;
  closest_approach_time: string;
  first_name: string | null;
  last_name: string | null;
  phone: string | null;
  email: string | null;
}) => {
  const name =
    (first_name ? first_name + " " : "") + (last_name ? last_name : "");
  return (
    <>
      <C.Td>
        <C.VStack fontSize="lg" alignItems="flex-start" spacing="0">
          <C.Text fontWeight="bold">{name}</C.Text>
          <C.Text fontSize="sm" opacity={0.6}>
            Drone ID: {id}
          </C.Text>
        </C.VStack>
      </C.Td>
      <C.Td fontSize="lg" textAlign="center">
        {Math.round(closest_approach / 10) / 100} m
      </C.Td>
      <C.Td fontSize="lg" textAlign="center">
        {format(new Date(closest_approach_time), "h:mm a")}
      </C.Td>
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

export default Violator;
