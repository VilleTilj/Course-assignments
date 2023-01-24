import Send from "../assets/icons/send.png";
import Shrug from "../assets/icons/shrug.png";
import Octopus from "../assets/icons/octopus.png";
import Mushroom from "../assets/icons/mushroom.png";
import Fire from "../assets/icons/fire.png";
import Tent from "../assets/icons/tent.png";

/**
 * Get icons
 * @returns
 */
function useIcons() {
  const icons = {
    send: Send,
    shrug: Shrug,
    octopus: Octopus,
    mushroom: Mushroom,
    fire: Fire,
    tent: Tent,
  };

  return icons;
}

export default useIcons;
