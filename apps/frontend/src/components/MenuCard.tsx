import type { MenuItem } from "@/types";
import { Badge } from "@/components/ui/badge";

interface Props {
  item: MenuItem;
  onClick?: () => void;
}

export default function MenuCard({ item, onClick }: Props) {
  return (
    <div
      onClick={onClick}
      className="flex cursor-pointer flex-col overflow-hidden rounded-xl border border-border bg-card transition-colors hover:border-primary"
    >
      {/* Image */}
      <div className="aspect-square w-full overflow-hidden bg-muted">
        {item.image_url ? (
          // eslint-disable-next-line @next/next/no-img-element
          <img
            src={item.image_url}
            alt={item.display_name}
            className="h-full w-full object-cover"
          />
        ) : (
          <div className="flex h-full items-center justify-center text-3xl text-muted-foreground">
            🍹
          </div>
        )}
      </div>

      {/* Info */}
      <div className="flex flex-1 flex-col gap-1 p-3">
        <p className="font-semibold leading-tight">{item.display_name}</p>
        {item.short_description && (
          <p className="line-clamp-2 text-xs text-muted-foreground">
            {item.short_description}
          </p>
        )}
        {item.tags.length > 0 && (
          <div className="mt-1 flex flex-wrap gap-1">
            {item.tags.slice(0, 3).map(({ tag }) => (
              <Badge key={tag.id} variant="outline" className="text-[10px] px-1.5 py-0">
                {tag.display_name}
              </Badge>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
