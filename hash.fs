open System.Security.Cryptography
open System.Collections.Generic

let printables = seq{for c in Seq.map char (seq{0..127}) do if not (System.Char.IsControl(c)) then yield c}

let rec product xss =
    match xss with
    | [] -> Seq.singleton Seq.empty
    | (xs::yss) -> seq{for p in (product yss) do for x in xs do yield Seq.append (Seq.singleton x) p }

let words = Seq.initInfinite (fun i -> List.replicate i printables |> product) |> Seq.concat |> Seq.map (fun x -> System.String.Join("", x))

let results = new Dictionary<byte list, byte[]>()

let pick_collision (i, (bytes, hash)) =
    if results.ContainsKey hash then
        Some(bytes, hash, results.[hash])
    else
        do
            ignore (results.Add(hash, bytes))
            if i%100000 = 0 then do
                printfn "%A" i
        None

let flag x = (log (float x) / log 2.0 + 1.0 |> int |> pown 2 )-1

let padded_byte x wbyte : seq<byte> =
    if x>0 then
        byte (flag x) &&& wbyte |> Seq.singleton
    else
        Seq.empty

let last_bits n (bytes: byte[]) =
    let l = bytes.Length
    let n_bytes = n/8
    let rem = n%8
    let wbyte = padded_byte rem bytes.[l-n_bytes-1]
    bytes |> Seq.skip (l - n_bytes) |> Seq.append wbyte |> Seq.toList

let find_collisions =
    let sha256 = new SHA256Managed()
    let encoding = new System.Text.ASCIIEncoding()
    let bytes = seq{for word in words -> encoding.GetBytes word}
    let hashes : seq<(int*(byte[]*byte list))> = seq{for bs in bytes -> bs, sha256.ComputeHash bs |> last_bits 40}|>Seq.zip (Seq.initInfinite id)
    let collision = Seq.pick pick_collision hashes
    let (first, hash, second) = collision
    encoding.GetString(first), encoding.GetString(second), hash

let main =
    printfn "%A" find_collisions

(*
how does this actually work? why the monadic "let!" ?

type Product () =
  member this.Bind (l,f) = List.collect f l
  member this.Return n = [n]

let enumeratedPizzas =
  Product() {
    let! x = ["New York";"Chicago"]
    let! y = ["Pepperoni";"Sausage"]
    let! z = ["Cheese";"Double Cheese"]
    return x,y,z
  }

*)